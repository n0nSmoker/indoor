import {
  USERS_ACTION_FETCH_USERS,
  USERS_ACTION_SET_FILTERS,
  USERS_ACTION_DELETE_USERS,
  USERS_ACTION_MUTATE_USERS,
} from './consts';


export const fetchUsers = () => ({ type: USERS_ACTION_FETCH_USERS });

export const deleteUser = userId => ({ type: USERS_ACTION_DELETE_USERS, payload: userId });

export const mutateUsers = (userData, callback) => ({ type: USERS_ACTION_MUTATE_USERS, payload: userData, callback });

export const setFilters = (filters) => ({ type: USERS_ACTION_SET_FILTERS, filters });
