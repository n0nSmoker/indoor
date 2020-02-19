import { all, call, put, select, takeLatest, takeEvery } from 'redux-saga/effects';

import { showNetworkError, showSuccess } from 'components/Notifications/actions';
import requests from 'lib/requests';

import { fetchPublishers } from './actions';
import {
  PUBLISHERS_ACTION_FETCH_PUBLISHERS,
  PUBLISHERS_ACTION_RECEIVE_PUBLISHERS,
  PUBLISHERS_ACTION_MUTATE_PUBLISHER,
  PUBLISHERS_ACTION_DELETE_PUBLISHER,
} from './consts';


function* fetchPublishersWorker() {
  try {
    const filters = yield select(
      ({publishersReducer: { filters }, headerReducer: { search }}) => ({
        ...filters,
        ...(search.value ? {query: search.value} : {}),
      })
    );
    const response = yield call(requests.get, '/publishers/', filters);
    yield put({type: PUBLISHERS_ACTION_RECEIVE_PUBLISHERS, publishers: response.data});
  } catch (e) {
    console.log(e);
    yield put(showNetworkError(e));
  }
}

function* mutatePublishersWorker({ payload: { id, ...formData }, callback }) {
  try {
    if(id) {
      yield call(requests.put, `/publishers/${id}/`, formData);
    } else {
      yield call(requests.post, '/publishers/', formData);
    }
    yield put(fetchPublishers());
    yield put(showSuccess(`Рекламодатель успешно ${id ? 'обновлен' : 'добавлен'}`));
    if (callback) callback();
  } catch (e) {
    yield put(showNetworkError(e))
  }
}

function* deletePublishersWorker(action) {
  try {
    yield call(requests.delete, `/publishers/${action.payload}/`);
    yield put(fetchPublishers());
    yield put(showSuccess('Рекламодатель успешно удален'));
  } catch (e) {
    yield put(showNetworkError(e));
  }
}

export default function* () {
  yield all([
    takeLatest(PUBLISHERS_ACTION_FETCH_PUBLISHERS, fetchPublishersWorker),
    takeLatest(PUBLISHERS_ACTION_MUTATE_PUBLISHER, mutatePublishersWorker),
    takeEvery(PUBLISHERS_ACTION_DELETE_PUBLISHER, deletePublishersWorker),
  ]);
}
