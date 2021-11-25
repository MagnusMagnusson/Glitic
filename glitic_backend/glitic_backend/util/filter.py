from rest_framework import filters

# A set of filters used to enhance the potential search and filter query parameters for models that it applies to. 
# The basefilter will search for a signal, which is the suffix of the querystring field mentioned, and will map it to a filterstring, which is what will be added to the django query.
# An example is that the detailedGTFilter will look for any querystring of format 'field_gt" and will then filter the queryset using the filter (field__gt = <query value>).

class DetailedBaseFilter(filters.BaseFilterBackend):
    signal = ""
    filterString = ""

    def get_filterset(self, view):
        return getattr(view, "filterset_fields")

    def get_matching_query(self, request, view):
        res = []
        filter_set = self.get_filterset(view)
        for field in filter_set:
            if (field+self.signal) in request.GET:
                res.append((field, request.GET[field+self.signal]))
        return res

    def filter_queryset(self, request, queryset, view):
        q = self.get_matching_query(request, view)
        filters = {}
        for match in q:
            filters[match[0]+self.filterString] = match[1]
        queryset = queryset.filter(**filters)
        return queryset

class DetailedExactFilter(DetailedBaseFilter):
    signal = ""
    filterString ="__iexact"

class DetailedLTFilter(DetailedBaseFilter):
    signal = "_lt"
    filterString = "__lt"

class DetailedGTFilter(DetailedBaseFilter):
    signal = "_gt"
    filterString = "__gt"

class DetailedContainsFilter(DetailedBaseFilter):
    signal = "_contains"
    filterString = "__icontains"

class DetailedStartsWithFilter(DetailedBaseFilter):
    signal = "_start"
    filterString = "__istartswith" 

class DetailedEndsWithFilter(DetailedBaseFilter):
    signal = "_iend"
    filterString = "__iendswith"

class DetailedExcludesFilter(DetailedBaseFilter):
    signal = "_not"
    def filter_queryset(self, request, queryset, view):
        q = self.get_matching_query(request, view)
        filters = {}
        for match in q:
            filters[match[0]+self.filterString] = match[1]
        queryset = queryset.exclude(**filters)
        return queryset

class DetailedInFilter(DetailedBaseFilter):
    signal="_in"
    filterString = "__in"

    def get_matching_query(self, request, view):
        res = []
        filter_set = self.get_filterset(view)
        for field in filter_set:
            if (field+self.signal) in request.GET:
                array = request.GET[field+self.signal].split(",")
                res.append((field, array))
        return res

class DetailedCompleteFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filters = [
            DetailedExactFilter,
            DetailedGTFilter,
            DetailedLTFilter,
            DetailedContainsFilter,
            DetailedStartsWithFilter,
            DetailedEndsWithFilter,
            DetailedExcludesFilter,
            DetailedInFilter,
        ]
        for filter in filters:
            inst = filter()
            queryset = inst.filter_queryset(request, queryset, view)
        return queryset