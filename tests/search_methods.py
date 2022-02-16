# -*- coding: utf-8 -*-

from macrobond_financial.common import Api, SearchFilter, StartOrEndPoint

from tests.test_common import TestCase


class Common(TestCase):

    def test_start_or_end_point(self) -> None:
        self.assertEqual(
            StartOrEndPoint.relative_to_observations(-1).__repr__(),
            '-1 mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            'StartOrEndPoint.relative_to_observations(-1).__repr__()'
        )

        self.assertEqual(
            str(StartOrEndPoint.relative_to_observations(-1)),
            '-1 mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            'StartOrEndPoint.relative_to_observations(-1).__str__()'
        )

        self.assertEqual(
            str(StartOrEndPoint.relative_to_years(-1)),
            '-1y mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            'StartOrEndPoint.relative_to_years(-1).__str__()'
        )

        self.assertEqual(
            str(StartOrEndPoint.relative_to_quarters(-1)),
            '-1q mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            'StartOrEndPoint.relative_to_quarters(-1).__str__()'
        )

        self.assertEqual(
            str(StartOrEndPoint.relative_to_months(-1)),
            '-1m mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            'StartOrEndPoint.relative_to_months(-1).__str__()'
        )

        self.assertEqual(
            str(StartOrEndPoint.relative_to_weeks(-1)),
            '-1w mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            'StartOrEndPoint.relative_to_weeks(-1).__str__()'
        )

        self.assertEqual(
            str(StartOrEndPoint.relative_to_days(-1)),
            '-1d mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            'StartOrEndPoint.relative_to_days(-1).__str__()'
        )

        self.assertEqual(
            str(StartOrEndPoint('-1', None)),
            '-1 mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            '(StartOrEndPoint(\'-1\', None).__str__()'
        )

        self.assertEqual(
            str(StartOrEndPoint.data_in_all_series()),
            ' mode:CalendarDateMode.DATA_IN_ALL_SERIES',
            'StartOrEndPoint.data_in_all_series()'
        )

        self.assertEqual(
            str(StartOrEndPoint.data_in_any_series()),
            ' mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            'StartOrEndPoint.data_in_any_series()'
        )

    def test_series_multi_filter(self) -> None:
        com = self.com_api.search.series_multi_filter(SearchFilter(text="usgdp"))
        web = self.web_api.search.series_multi_filter(SearchFilter(text="usgdp"))

        self.assertEqual(
            len(com.entities), len(web.entities),
            'len(com.entities) == len(web.entities)'
        )

        self.assertNotEqual(len(com.entities), 0, 'len(com.entities) != 0')

        com_first = com.entities[0]
        web_first = web.entities[0]

        self.assertEqual(str(com_first), str(web_first), '__str__()')
        # self.assertEqual(com_first.__repr__(), web_first.__repr__(), '__repr__()')
        self.assertEqual(com_first.name, web_first.name, 'name')
        self.assertEqual(com_first.primary_name, web_first.primary_name, 'primary_name')
        self.assertEqual(com_first.title, web_first.title, 'title')
        self.assertEqual(com_first.is_error, web_first.is_error, 'is_error')
        self.assertEqual(com_first.error_message, web_first.error_message, 'error_message')


class Web(TestCase):

    def test_search(self) -> None:
        search(self, self.web_api)

    def test_series_multi_filter(self) -> None:
        series_multi_filter(self, self.web_api)

    def test_series_multi_filter_must_have_attributes(self) -> None:
        series_multi_filter_must_have_attributes(self, self.web_api)

    def test_series_multi_filter_must_not_have_attributes(self) -> None:
        series_multi_filter_must_not_have_attributes(self, self.web_api)

    def test_series_multi_filter_must_have_values(self) -> None:
        series_multi_filter_must_have_values(self, self.web_api)

    def test_series_multi_filter_must_not_have_values(self) -> None:
        series_multi_filter_must_not_have_values(self, self.web_api)

    def test_web_series_multi_filter_include_discontinued(self) -> None:
        series_multi_filter_include_discontinued(self, self.web_api)

    def test_series_multi_filter_entity_types(self) -> None:
        series_multi_filter_entity_types(self, self.web_api)


class Com(TestCase):

    def test_search(self) -> None:
        search(self, self.com_api)

    def test_series_multi_filter(self) -> None:
        series_multi_filter(self, self.com_api)

    def test_series_multi_filter_must_have_attributes(self) -> None:
        series_multi_filter_must_have_attributes(self, self.com_api)

    def test_series_multi_filter_must_not_have_attributes(self) -> None:
        series_multi_filter_must_not_have_attributes(self, self.com_api)

    def test_series_multi_filter_must_have_values(self) -> None:
        series_multi_filter_must_have_values(self, self.com_api)

    def test_series_multi_filter_must_not_have_values(self) -> None:
        series_multi_filter_must_not_have_values(self, self.com_api)

    def test_web_series_multi_filter_include_discontinued(self) -> None:
        series_multi_filter_include_discontinued(self, self.com_api)

    def test_series_multi_filter_entity_types(self) -> None:
        series_multi_filter_entity_types(self, self.com_api)


def search(test: TestCase, api: Api) -> None:
    search_result = api.search.search(text="usgdp")

    test.assertNotEqual(len(search_result.entities), 0, 'len(search_result.entities) != 0')
    first = search_result.entities[0]

    test.assertNotEqual(
        len(first.metadata), 0,
        'len(first.metadata) != 0'
    )


def series_multi_filter(test: TestCase, api: Api) -> None:
    search_result = api.search.series_multi_filter(SearchFilter(text="usgdp"))

    test.assertNotEqual(len(search_result.entities), 0, 'len(search_result.entities) != 0')
    first = search_result.entities[0]

    test.assertNotEqual(
        len(first.metadata), 0,
        'len(first.metadata) != 0'
    )


def series_multi_filter_must_have_attributes(test: TestCase, api: Api) -> None:
    search_result = api.search.series_multi_filter(
        SearchFilter(must_have_attributes=["MoveBase"])
    )

    test.assertNotEqual(len(search_result.entities), 0, 'len(com.entities) != 0')

    for entitie in search_result.entities:
        if 'MoveBase' not in entitie.metadata:
            test.fail('MoveBase not in ' + entitie.name)


def series_multi_filter_must_not_have_attributes(test: TestCase, api: Api) -> None:
    search_result = api.search.series_multi_filter(
        SearchFilter(must_not_have_attributes=["MoveBase"])
    )

    test.assertNotEqual(len(search_result.entities), 0, 'len(com.entities) != 0')

    for entitie in search_result.entities:
        if 'MoveBase' in entitie.metadata:
            test.fail('MoveBase is in ' + entitie.name)


def series_multi_filter_must_have_values(test: TestCase, api: Api) -> None:
    search_result = api.search.series_multi_filter(
        SearchFilter(must_have_values={"MoveBase": 'pp100'})
    )

    test.assertNotEqual(len(search_result.entities), 0, 'len(com.entities) != 0')

    for entitie in search_result.entities:
        test.assertEqual(
            entitie.metadata.get('MoveBase'),
            'pp100',
            'MoveBase != "pp100" ' + entitie.name
        )


def series_multi_filter_must_not_have_values(test: TestCase, api: Api) -> None:
    search_result = api.search.series_multi_filter(
        SearchFilter(must_not_have_values={"MoveBase": 'pp100'})
    )

    test.assertNotEqual(len(search_result.entities), 0, 'len(com.entities) != 0')

    for entitie in search_result.entities:
        test.assertNotEqual(
            entitie.metadata.get('MoveBase'),
            'pp100',
            'MoveBase != "pp100" ' + entitie.name
        )


def series_multi_filter_include_discontinued(test: TestCase, api: Api) -> None:
    text = 's_07707'

    include = api.search.series_multi_filter(
        SearchFilter(text=text),
        include_discontinued=True,
    )

    not_include = api.search.series_multi_filter(
        SearchFilter(text=text),
        include_discontinued=False,
    )

    test.assertNotEqual(len(include), 6000, 'len(include) != 6000')
    test.assertNotEqual(len(not_include), 6000, 'len(not_include) != 6000')

    test.assertNotEqual(len(include), 0, 'len(include) != 0')
    test.assertNotEqual(len(not_include), 0, 'len(not_include) != 0')

    test.assertGreater(len(include), len(not_include), 'include > not_include')


def series_multi_filter_entity_types(test: TestCase, api: Api) -> None:
    text = 'abc'

    security = api.search.series_multi_filter(
        SearchFilter(text=text, entity_types=['Security'])
    )

    test.assertNotEqual(len(security), 0, 'len(security) != 0')

    for entitie in security.entities:
        test.assertEqual(
            entitie.entity_type, 'Security', 'EntityType != "Security" ' + entitie.name
        )
