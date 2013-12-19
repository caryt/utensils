"""Testing Utensils
===================
"""
from __future__                         import print_function
from unittest import TestCase, TestLoader
from HTMLTestRunner import HTMLTestRunner as Runner
from os.path import join, abspath


class MultipleTests(TestCase):
    """A Test Case that can automatically generate a number of Tests."""

    @classmethod
    def fn_name(cls, check_fn, args, result):
        """Return a name for the check_fn for an individual test. (NB: must start with "test")."""
        name = "test_%s_%r_%r" % (check_fn.__name__, args, result)
        return name.translate(None, "<>()',").replace(' ', '_').replace(".", "_")

    @classmethod
    def generate_test(cls, check_fn, args, result):
        """Generate an individual test, and add it to this TestCase."""
        setattr(cls, cls.fn_name(check_fn, args, result), lambda self: check_fn(self, args, result))


class HTMLTestRunner(Runner):
    """HTMLTest Runner."""
    def parse_failure(self, failure):
        """Convenience routine to extract the Location and Assertion message
        from a test failure."""
        lastLine = failure[1].split('\n')[-2]
        return {'loc': failure[0], 'error': lastLine}

    def run(self, testsuite):
        """Run the testsuite, saving report to fname."""
        self.fname = join(abspath('.'), 'testResults.html')
        with file(self.fname, 'wb') as fp:
            runner = Runner(
                stream      = fp,
                title       = 'Unit Tests',
                description = 'Summary of Test Run.',
            )
            results = runner.run(testsuite)
            self.print_summary(results)
        return results


    def print_summary(self, results):
        """Summarise the results."""
        for f in results.failures:
            print('{loc:60} {error}'.format(**(self.parse_failure(f))))
        print(results)
        print('For details see file://{}'.format(self.fname))
