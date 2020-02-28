import { FETCH_CURRENT_USER, RECEIVE_CURRENT_USER } from './consts'


export default (state = {
  currentUser: null,
  isLoading: true,
}, action) => {
  switch (action.type) {
    case FETCH_CURRENT_USER:
      return {
        ...state,
        isLoading: true,
      };
    case RECEIVE_CURRENT_USER:
      const { payload } = action;
      return {
        ...state,
        isLoading: false,
        currentUser: payload,
      };
    default:
      return state;
  }
};
