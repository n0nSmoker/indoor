import {
  DEVICES_ACTION_RECEIVE_DEVICES,
  DEVICES_ACTION_SET_FILTERS,
  LOCATIONS_ACTION_RECEIVE_LOCATIONS,
} from './consts';

const devices = (state = {
  devices: [],
  total: 0,
  isLoading: false,
  cities: [],
  locations: [],
  filters: {
    limit: 10,
    page: 1
  },
}, action) => {
  switch (action.type) {
    case DEVICES_ACTION_SET_FILTERS:
      return {
        ...state,
        filters: action.filters,
      };
    case DEVICES_ACTION_RECEIVE_DEVICES:
      return {
        ...state,
        devices: action.devices.results,
        total: action.devices.total,
        cities: action.cities.results,
      };
    case LOCATIONS_ACTION_RECEIVE_LOCATIONS:
      return {
        ...state,
        locations: action.locations.results,
      };
    default:
      return state;
  }
};

export default devices;
