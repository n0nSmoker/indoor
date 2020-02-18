import {
  NOTIFICATION_ACTION_SHOW_MESSAGE,
  NOTIFICATION_ACTION_CLOSE,
} from './consts';


export const showMessage = (message, variant) => ({ type: NOTIFICATION_ACTION_SHOW_MESSAGE, payload: { message, variant } });
export const showSuccess = message => showMessage(message, 'success');
export const showWarning = message => showMessage(message, 'warning');
export const showError = message => showMessage(message, 'error');
export const showInfo = message => showMessage(message, 'info');

export const showNetworkError = ({ response }) => {
  let message = 'Ошибка сервера!';
  if (response && response.status === 400) {
    if (response.data && response.data.errors) {
      message = response.data.errors.join('\n');
    }
  }
  return showError(message);
};

export const closeAction = () => ({ type: NOTIFICATION_ACTION_CLOSE });
