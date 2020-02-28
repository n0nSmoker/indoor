import { call, put, all, takeLatest } from 'redux-saga/effects';

import { showNetworkError } from 'components/Notifications/actions';
import requests from 'lib/requests';

import { FETCH_CURRENT_USER, RECEIVE_CURRENT_USER } from './consts'


function* fetchCurrentUserWorker() {
  try {
    const response = yield call(requests.get, '/users/current/');
    yield put({ type: RECEIVE_CURRENT_USER, payload: response.data });
  } catch (e) {
    yield put(showNetworkError(e));
  }
}

export default function* () {
  yield all([
    takeLatest(FETCH_CURRENT_USER, fetchCurrentUserWorker),
  ]);
};
