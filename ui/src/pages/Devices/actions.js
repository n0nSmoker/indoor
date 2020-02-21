import {
  DEVICES_ACTION_FETCH_DEVICES,
  DEVICES_ACTION_SET_FILTERS,
  DEVICES_ACTION_MUTATE_DEVICES,
  LOCATIONS_ACTION_FETCH_LOCATIONS,
} from './consts';


export const fetchDevices = () => ({ type: DEVICES_ACTION_FETCH_DEVICES });

export const mutateDevices = (deviceData, callback) => ({
  type: DEVICES_ACTION_MUTATE_DEVICES,
  payload: deviceData, callback
});

export const setFilters = (filters) => ({ type: DEVICES_ACTION_SET_FILTERS, filters });

export const fetchLocations = cityId => ({ type: LOCATIONS_ACTION_FETCH_LOCATIONS, payload: cityId });
