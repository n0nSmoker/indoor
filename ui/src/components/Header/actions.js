import { HEADER_ACTION_SET, HEADER_ACTION_SET_SEARCH_VALUE } from './consts';

export const setHeader = settings => ({ type: HEADER_ACTION_SET, payload: settings });
export const setSearchValue = value => ({ type: HEADER_ACTION_SET_SEARCH_VALUE, payload: value });
