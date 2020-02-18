import { all, call, put, select, takeLatest, takeEvery } from 'redux-saga/effects';

import requests from '../../lib/requests.js';

import {
  CONTENT_ACTION_FETCH_CONTENT,
  CONTENT_ACTION_RECEIVE_CONTENT,
  CONTENT_ACTION_ADD_CONTENT,
  CONTENT_ACTION_UPDATE_CONTENT,
  CONTENT_ACTION_DELETE_CONTENT,
} from './consts.js';

function* fetchContentWorker() {
  const filters = yield select(state => state.contentReducer.filters);
  const response = yield call(requests.get, '/content/', filters);
  yield put({type: CONTENT_ACTION_RECEIVE_CONTENT, content: response.data});
}

function* addContentWorker(action) {
  const headers = {
      'Content-Type': 'multipart/form-data',
  };
  yield call(requests.post, '/content/', action.formData, headers );
  if (action.callback) action.callback();
}

function* updateContentWorker(action) {
   const headers = {
      'Content-Type': 'multipart/form-data',
  };
  yield call(requests.put, `/content/${action.contentId}/`, action.formData, headers);
  if (action.callback) action.callback();
}

function* deleteContentWorker(action) {
  yield call(requests.delete, `/content/${action.contentId}/`);
  if (action.callback) action.callback();
}

export default function* () {
  yield all([
    takeLatest(CONTENT_ACTION_FETCH_CONTENT, fetchContentWorker),
    takeLatest(CONTENT_ACTION_ADD_CONTENT, addContentWorker),
    takeLatest(CONTENT_ACTION_UPDATE_CONTENT, updateContentWorker),
    takeEvery(CONTENT_ACTION_DELETE_CONTENT, deleteContentWorker),
  ]);
}
