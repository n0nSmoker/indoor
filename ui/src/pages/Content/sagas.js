import { all, call, put, select, takeLatest, takeEvery } from 'redux-saga/effects';

import { showNetworkError, showSuccess } from 'components/Notifications/actions';
import requests from '../../lib/requests.js';

import { fetchContent } from './actions';
import {
  CONTENT_ACTION_FETCH_CONTENT,
  CONTENT_ACTION_RECEIVE_CONTENT,
  CONTENT_ACTION_MUTATE_CONTENT,
  CONTENT_ACTION_DELETE_CONTENT,
} from './consts.js';


function* fetchContentWorker() {
  try {
    const filters = yield select(
      ({contentReducer: { filters }, headerReducer: { search }}) => ({
        ...filters,
        ...(search.value ? {query: search.value} : {}),
      })
    );
    const response = yield call(requests.get, '/content/', filters);
    yield put({type: CONTENT_ACTION_RECEIVE_CONTENT, content: response.data});
  } catch (e) {
    yield put(showNetworkError(e))
  }
}

function* mutateContentWorker({ payload: { id, formData }, callback}) {
  const headers = {
       'Content-Type': 'multipart/form-data',
  };
  try {
    if (id) {
      yield call(requests.put, `/content/${id}/`, formData, headers );
    } else {
      yield call(requests.post, '/content/', formData, headers );
    }
    yield put(fetchContent());
    yield put(showSuccess(`Контент успешно ${id ? 'обновлен' : 'добавлен'}`));
    if (callback) callback();
  } catch (e) {
    yield put(showNetworkError(e));
  }
}

function* deleteContentWorker(action) {
  try {
    yield call(requests.delete, `/content/${action.contentId}/`);
    yield put(fetchContent());
    yield put(showSuccess('Контент успешно удален'));
  } catch (e) {
    yield put(showNetworkError(e));
  }
}


export default function* () {
  yield all([
    takeLatest(CONTENT_ACTION_FETCH_CONTENT, fetchContentWorker),
    takeLatest(CONTENT_ACTION_MUTATE_CONTENT, mutateContentWorker),
    takeEvery(CONTENT_ACTION_DELETE_CONTENT, deleteContentWorker),
  ]);
}
