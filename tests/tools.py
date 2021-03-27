from nose.tools import *
import re


def assert_response(resp, contains=None, matches=None, headers=None, status='200'):
	assert status in resp.status, f'Expected response {status} not in {resp.status}'

	if status == '200':
		assert resp.data, 'Response data is empty'

	if contains:
		assert contains.encode() in resp.data, f'Response does not contain {contains}'

	if matches:
		reg = re.compile(matches)
		assert reg.matches(resp.data), f'Response does not match {matches}'

	if headers:
		assert_equal(resp.headers, headers)
