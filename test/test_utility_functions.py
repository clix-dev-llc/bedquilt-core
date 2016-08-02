import testutils
import json
import psycopg2


class TestSplitQueries(testutils.BedquiltTestCase):

    def _assert_examples(self, examples):
        for query, match, specials in examples:
            result = self._query("""
            select * from bq_split_queries('{}'::jsonb)
            """.format(json.dumps(query)))
            self.assertEqual(json.loads(result[0][0]), match)
            self.assertEqual(result[0][1], specials)

    def test_simple_queries_with_no_specials(self):

        examples = [
            ({'a': {'b': 1}},
             {'a': {'b': 1}},
             []),
            ({'a': 1, 'b': 2},
             {'a': 1, 'b': 2},
             [])
        ]

        self._assert_examples(examples)

    def test_advanced_queries(self):
        examples = [
            (
                {
                    'a': {
                        'b': {
                            '$eq': 22
                        }
                    }
                },
                {},
                ["and bq_jdoc #> '{a,b}' = '22'::jsonb"]
            ),
            (
                {
                    'a': {
                        'b': {
                            '$eq': 22
                        }
                    },
                    'c': 44
                },
                {
                    'c': 44
                },
                ["and bq_jdoc #> '{a,b}' = '22'::jsonb"]
            ),
            (
                {
                    'a': {
                        'b': {
                            '$eq': 22
                        },
                        'c': 44
                    }
                },
                {
                    'a': {'c': 44}
                },
                ["and bq_jdoc #> '{a,b}' = '22'::jsonb"]
            )
        ]

        self._assert_examples(examples)

    def test_supported_ops(self):
        examples = [
            (
                {'a': {'b': {'$eq': 42}}},
                {},
                ["and bq_jdoc #> '{a,b}' = '42'::jsonb"]
            ),
            (
                {'a': {'b': {'$noteq': 42}}},
                {},
                ["and bq_jdoc #> '{a,b}' != '42'::jsonb"]
            ),
            (
                {'a': {'b': {'$gte': 42}}},
                {},
                ["and bq_jdoc #> '{a,b}' >= '42'::jsonb"]
            ),
            (
                {'a': {'b': {'$gt': 42}}},
                {},
                ["and bq_jdoc #> '{a,b}' > '42'::jsonb"]
            ),
            (
                {'a': {'b': {'$lte': 42}}},
                {},
                ["and bq_jdoc #> '{a,b}' <= '42'::jsonb"]
            ),
            (
                {'a': {'b': {'$lt': 42}}},
                {},
                ["and bq_jdoc #> '{a,b}' < '42'::jsonb"]
            ),
            (
                {'a': {'b': {'$in': [22, 42]}}},
                {},
                ["and bq_jdoc #> '{a,b}' <@ '[22, 42]'::jsonb"]
            ),
        ]

        self._assert_examples(examples)
