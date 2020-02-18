import {
  NOTIFICATION_ACTION_SHOW_MESSAGE,
  NOTIFICATION_ACTION_CLOSE,
} from './consts';


const initialDuration = 3000;
const notification = (state = {
  open: false,
  message: '',
  duration: initialDuration,
  variant: null,
}, action) => {
  switch (action.type) {
    case NOTIFICATION_ACTION_SHOW_MESSAGE:
      return {
        ...state,
        ...action.payload,
        open: true,
      };
    case NOTIFICATION_ACTION_CLOSE:
      return {
        ...state,
        open: false,
        duration: initialDuration,
      };
    default:
      return state;
  }
};

export default notification;
