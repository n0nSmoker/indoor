import {
  PUBLISHERS_ACTION_SET_FILTERS,
  PUBLISHERS_ACTION_RECEIVE_PUBLISHERS,
} from './consts.js'


const publishers = (state = {
  publishers: [],
  total: 0,
  isLoading: false,
  filters: {
    limit: 10,
    page: 1,
  },
}, action) => {
  switch (action.type) {
    case PUBLISHERS_ACTION_SET_FILTERS:
      return {
        ...state,
        filters: action.filters,
      };
    case PUBLISHERS_ACTION_RECEIVE_PUBLISHERS:
      return {
        ...state,
        publishers: action.publishers.results,
        total: action.publishers.total,
      };
    default:
      return state;
  }
};

export default publishers;
