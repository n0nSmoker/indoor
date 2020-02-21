import { all, call, put, select, takeLatest } from 'redux-saga/effects';

import { showNetworkError, showSuccess } from 'components/Notifications/actions';
import requests from 'lib/requests';

import { fetchDevices } from './actions';
import { fetchLocations } from './actions';

import {
  DEVICES_ACTION_FETCH_DEVICES,
  DEVICES_ACTION_RECEIVE_DEVICES,
  DEVICES_ACTION_MUTATE_DEVICES,
  LOCATIONS_ACTION_FETCH_LOCATIONS,
  LOCATIONS_ACTION_RECEIVE_LOCATIONS,
  LOCATIONS_ACTION_MUTATE_LOCATIONS,
} from './consts';


function* fetchDevicesWorker() {
  try {
    const filters = yield select(
      ({ devicesReducer: { filters }, headerReducer: { search }}) => ({
        ...filters,
        ...(search.value ? { query: search.value } : {}),
      })
    );
    const devicesResponse = yield call(requests.get, '/devices/', filters);
    const citiesResponse = yield call(requests.get, '/locations/cities/');
    const locationsResponse = yield call(requests.get, '/locations/');
    yield put({
      type: DEVICES_ACTION_RECEIVE_DEVICES,
      devices: devicesResponse.data,
      locations: locationsResponse.data,
      cities: citiesResponse.data,
    });
  } catch (e) {
    yield put(showNetworkError(e))
  }
}

function* fetchLocationsWorker(action) {
  try {
    const response = yield call(requests.get, `/locations/${action.payload}/`);
    yield put({ type: LOCATIONS_ACTION_RECEIVE_LOCATIONS, locations: response.data});
  } catch (e) {
    yield put(showNetworkError(e))
  }
}

function* mutateDevicesWorker({ payload: { id, ...formData }, callback }) {
  try {
    yield call(requests.put, `/devices/${id}/`, formData);
    yield put(fetchDevices());
    yield put(showSuccess(`Девайс успешно обновлен`));
    if (callback) callback();
  } catch (e) {
    yield put(showNetworkError(e));
  }
}

function* mutateLocationsWorker({ payload: { ...formData }, callback }) {
  try {
    yield call(requests.post, `/locations/`, formData);
    yield put(fetchLocations(formData.city_id));
    if (callback) callback();
  } catch (e) {
    yield put(showNetworkError(e));
  }
}

export default function* () {
  yield all([
    takeLatest(DEVICES_ACTION_FETCH_DEVICES, fetchDevicesWorker),
    takeLatest(LOCATIONS_ACTION_FETCH_LOCATIONS, fetchLocationsWorker),
    takeLatest(DEVICES_ACTION_MUTATE_DEVICES, mutateDevicesWorker),
    takeLatest(LOCATIONS_ACTION_MUTATE_LOCATIONS, mutateLocationsWorker),
  ])
}
