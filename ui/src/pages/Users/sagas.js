import { all, call, put, select, takeLatest } from 'redux-saga/effects';

import { showNetworkError, showSuccess } from 'components/Notifications/actions';
import requests from 'lib/requests';

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
    yield put(showNetworkError(e));
  }
}

function* deleteUsersWorker(action) {
  try {
    yield call(requests.delete, `/users/${action.payload}/`);
    yield put(fetchUsers());
    yield put(showSuccess('Пользователь успешно удален'));
  } catch (e) {
    yield put(showNetworkError(e));
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
    yield put(showSuccess(`Пользователь успешно ${id ? 'обновлен' : 'добавлен'}`));
    if (callback) callback();
  } catch (e) {
    yield put(showNetworkError(e));
  }
}


export default function* () {
  yield all([
    takeLatest(USERS_ACTION_FETCH_USERS, fetchUsersWorker),
    takeLatest(USERS_ACTION_DELETE_USERS, deleteUsersWorker),
    takeLatest(USERS_ACTION_MUTATE_USERS, mutateUsersWorker),
  ]);
}
