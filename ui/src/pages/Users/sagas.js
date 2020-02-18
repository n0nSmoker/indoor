import { all, call, put, select, takeLatest } from 'redux-saga/effects';

import requests from '../../lib/requests';

import { fetchUsers } from './actions';
import {
  USERS_ACTION_FETCH_USERS,
  USERS_ACTION_RECEIVE_USERS,
  USERS_ACTION_DELETE_USERS,
  USERS_ACTION_MUTATE_USERS,
} from './consts';


function* fetchUsersWorker() {
  try {
    const filters = yield select(
      ({usersReducer: { filters }, headerReducer: { search }}) => ({
        ...filters,
        ...(search.value ? {query: search.value} : {}),
      })
    );
    const response = yield call(requests.get, '/users/', filters);
    yield put({type: USERS_ACTION_RECEIVE_USERS, users: response.data});
  } catch (e) {
    // TODO: put notifications action
    console.error(e);
  }
}

function* deleteUsersWorker(action) {
  try {
    yield call(requests.delete, `/users/${action.payload}`);
    yield put(fetchUsers())
  } catch (e) {
    // TODO: put notifications action
    console.error(e);
  }
}

function* mutateUsersWorker({ payload: { id, ...formData }, callback}) {
  try {
    if (id) {
      yield call(requests.put,`/users/${id}/`, formData)
    } else {
      yield call(requests.post, '/users/', formData)
    }
    yield put(fetchUsers());
    if (callback) callback();
  } catch (e) {
    // TODO: put notifications action
    console.error(e);
  }
}


export default function* () {
  yield all([
    takeLatest(USERS_ACTION_FETCH_USERS, fetchUsersWorker),
    takeLatest(USERS_ACTION_DELETE_USERS, deleteUsersWorker),
    takeLatest(USERS_ACTION_MUTATE_USERS, mutateUsersWorker),
  ]);
}
