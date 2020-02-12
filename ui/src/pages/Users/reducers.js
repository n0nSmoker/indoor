import {
  USERS_ACTION_SET_FILTERS,
  USERS_ACTION_RECEIVE_USERS,
} from './consts';


const users = (state = {
  users: [],
  total: 0,
  isLoading: false,
  filters: {
    limit: 10,
    page: 1,
  },
}, action) => {
  switch (action.type) {
    case USERS_ACTION_SET_FILTERS:
      return {
        ...state,
        filters: action.filters,
      };
    case USERS_ACTION_RECEIVE_USERS:
      return {
        ...state,
        users: action.users.results,
        total: action.users.total,
      };
    default:
      return state;
  }
};

export default users;
