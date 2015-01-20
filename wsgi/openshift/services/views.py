from django.shortcuts import render

# Create your views here.
from .models import Message, Usage
from rest_framework import response, views, viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .serializer import MessageSerializer, UsageSerializer
import django_filters
from rest_framework import generics
from rest_framework.reverse import reverse
import datetime
import hashlib
import settings

OS_NAMES = ['Linux', 'Windows NT', 'Darwin']
UTC = datetime.tzinfo('UTC')

class MessageViewSet(viewsets.ModelViewSet):
  queryset = Message.objects.all()
  serializer_class = MessageSerializer
  permission_classes = [IsAuthenticatedOrReadOnly]

class WithinDateFilter(django_filters.DateFilter):
    def filter(self, queryset, value):
        from datetime import timedelta
        if value:
            # date_value = value.replace(hour=0, minute=0, second=0)
            filter_lookups = {
                "%s__range" % (self.name, ): (
                    value,
                    value + timedelta(days=1),
                ),
            }
            queryset = queryset.filter(**filter_lookups)
        return queryset

class MD5Filter(django_filters.CharFilter):
    def filter(self, queryset, value):
        if value:
            if len(value) != 32:
                value = hashlib.md5(value).hexdigest()
            filter_lookups = { self.name: value }
            queryset = queryset.filter(**filter_lookups)
        return queryset

class UsageFilter(django_filters.FilterSet):
    date    = WithinDateFilter(name="dateTime")
    datemin = django_filters.DateFilter(name="dateTime", lookup_type='gte')
    datemax = django_filters.DateFilter(name="dateTime", lookup_type='lt')
    uid = MD5Filter(name="uid")
    host = MD5Filter(name="host")

    class Meta:
        model = Usage
        fields = ['date', 'datemin','datemax', 'osName']
        order_by = ['-dateTime']

class UsageViewSet(viewsets.ModelViewSet):
  """All usages registered in the system. Valid filter parameters are:
    'host', 'uid', 'datemin', 'datemax', and 'date'.
  """
  queryset = Usage.objects.all()
  serializer_class = UsageSerializer
  permission_classes = [AllowAny]
  filter_class=UsageFilter


def filterByDate(queryset, request=None, datemin=None, datemax=None):
    if request:
        datemin = request.GET.get("datemin", datemin)
        datemax = request.GET.get("datemax", datemax)
        # datemax = request.data.get("datemax", datemax)
        # datemax = request.data.get("datemax", datemax)

    if datemin:
        queryset = django_filters.DateFilter(name="dateTime", lookup_type='gte').filter(queryset, datemin)

    if datemax:
        queryset = django_filters.DateFilter(name="dateTime", lookup_type='lt').filter(queryset, datemax)

    return queryset

def getDateRange(queryset):
    queryset = queryset.order_by("dateTime")
    dates=[]
    delta = datetime.timedelta(days=1)
    item = queryset.first().dateTime.date()
    end = queryset.last().dateTime.date()
    while item <= end:
        dates.append(item)
        item += delta
    return dates

def prepResult(dates):
    result = {'date':dates, 'total':[], 'other':[]}
    for label in OS_NAMES:
        result[label] = []
    return result

def convertResult(result):
    mapping = {'Linux':'linux', 'Darwin':'mac', 'Windows NT':'windows'}
    for key in mapping.keys():
        if key in result:
          result[mapping[key]] = result.pop(key)
    return result

@api_view(('GET',))
def host_list(request, format=None):
  """List of hosts. This can be filtered with 'datemin' and 'datemax' parameters"""
  queryset = Usage.objects.all()
  queryset = filterByDate(queryset, request)

  hosts = []
  host_names = []
  # only return the values that are actually used - sort by most recent first
  for host in queryset.order_by("-dateTime")\
         .values('host', 'osReadable', 'osName', 'osArch', 'osVersion', 'dateTime'):
      if not host['host'] in host_names:
          host_names.append(host['host'])
          hosts.append(host)

  return response.Response(hosts)

@api_view(('GET',))
def user_list(request, format=None):
    """List of users. This can be filtered with 'datemin' and 'datemax' parameters"""
    queryset = Usage.objects.all()
    queryset = filterByDate(queryset, request)

    uids = []
    uid_names = []
    for uid in queryset.order_by("-dateTime")\
          .values('uid', 'dateTime'):
        if not uid['uid'] in uid_names:
            uid_names.append(uid['uid'])
            uids.append(uid)

    return response.Response(uids)

def query_count(queryset, field):
    if field:
        return queryset.order_by(field).values(field).distinct().count()
    else:
        return queryset.count()

def usage_by_field(request, format=None, field=None):
    queryset = filterByDate(Usage.objects.all(), request)
    dates = getDateRange(queryset)
    result = prepResult(dates)

    dateFilter = WithinDateFilter('dateTime')
    for date in dates:
        queryset_date = dateFilter.filter(queryset, date)
        total = query_count(queryset_date, field)
        cumulative = 0
        for label in OS_NAMES:
            count = query_count(queryset_date.filter(osName=label), field)
            cumulative += count
            result[label].append(count)
        result['total'].append(total)
        result['other'].append(max(0,total-cumulative)) # one user can be on multiple systems

    result = convertResult(result)

    # make the result look like a d3.csv load
    finalResult = []
    for i in xrange(len(result['date'])):
        line = {}
        for key in result.keys():
            line[key] = result[key][i]
        finalResult.append(line)

    return response.Response(finalResult)

@api_view(('GET',))
def usage_by_hosts(request, format=None):
    return usage_by_field(request, format, 'host')

@api_view(('GET',))
def usage_by_users(request, format=None):
    return usage_by_field(request, format, 'uid')

@api_view(('GET',))
def usage_by_start(request, format=None):
    return usage_by_field(request, format)

@api_view(('GET',))
def api_root(request, format=None):
    return response.Response({
        'by':    reverse('by-root',    request=request, format=format),
        'host':  reverse('host-list',  request=request, format=format),
        'usage': reverse('usage-list', request=request, format=format),
        'user':  reverse('user-list',  request=request, format=format)
    })

@api_view(('GET',))
def by_root(request, format=None):
    return response.Response({
        'host':reverse('by-hosts', request=request, format=format),
        'user':reverse('by-users', request=request, format=format),
        'start':reverse('by-starts', request=request, format=format),
    })
