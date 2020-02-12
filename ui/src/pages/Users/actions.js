import { USERS_ACTION_FETCH_USERS, USERS_ACTION_SET_FILTERS } from './consts';


export const fetchUsers = () => ({ type: USERS_ACTION_FETCH_USERS });
export const setFilters = (filters) => ({ type: USERS_ACTION_SET_FILTERS, filters });
