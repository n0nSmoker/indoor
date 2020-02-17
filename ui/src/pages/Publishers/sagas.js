import { all, call, put, select, takeLatest, takeEvery } from 'redux-saga/effects';

import requests from '../../lib/requests.js';

import {
  PUBLISHERS_ACTION_FETCH_PUBLISHERS,
  PUBLISHERS_ACTION_RECEIVE_PUBLISHERS,
  PUBLISHERS_ACTION_ADD_PUBLISHER,
  PUBLISHERS_ACTION_UPDATE_PUBLISHER,
  PUBLISHERS_ACTION_DELETE_PUBLISHER,
} from './consts.js';

function* fetchPublishersWorker() {
  const filters = yield select(state => state.publishersReducer.filters);
  const response = yield call(requests.get, '/publishers/', filters);
  yield put({type: PUBLISHERS_ACTION_RECEIVE_PUBLISHERS, publishers: response.data})
}

function* addPublisherWorker(action) {
  yield call(requests.post, '/publishers/', action.formData);
  if (action.callback) action.callback();
}

function* updatePublisherWorker(action) {
  yield call(requests.put, `/publishers/${action.publisherId}/`, action.formData);
  if (action.callback) action.callback();
}

function* deletePublisherWorker(action) {
  yield call(requests.delete, `/publishers/${action.publisherId}/`);
  if (action.callback) action.callback();
}

export default function* () {
  yield all([
    takeLatest(PUBLISHERS_ACTION_FETCH_PUBLISHERS, fetchPublishersWorker),
    takeLatest(PUBLISHERS_ACTION_ADD_PUBLISHER, addPublisherWorker),
    takeLatest(PUBLISHERS_ACTION_UPDATE_PUBLISHER, updatePublisherWorker),
    takeEvery(PUBLISHERS_ACTION_DELETE_PUBLISHER, deletePublisherWorker),
  ]);
}
