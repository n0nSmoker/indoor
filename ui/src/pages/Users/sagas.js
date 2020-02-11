import { all, call, put, select, takeLatest } from 'redux-saga/effects';

import requests from '../../lib/requests';

import {
  USERS_ACTION_FETCH_USERS,
  USERS_ACTION_RECEIVE_USERS,
} from './consts';


function* fetchUsersWorker() {
  const filters = yield select(state => state.usersReducer.filters);
  const response = yield call(requests.get, '/users/', filters);
  yield put({ type: USERS_ACTION_RECEIVE_USERS, users: response.data });
}


export default function* () {
  yield all([
    takeLatest(USERS_ACTION_FETCH_USERS, fetchUsersWorker),
  ]);
}
