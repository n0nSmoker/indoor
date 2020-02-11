import axios from 'axios';


function errorHandler(err) {
  const { response } = err;
  switch (response.status) {
    case 403:
      window.location = '/';
      break;
    case 400:
      console.dir(response.data);
      break;
    default:
      // TODO: notifications
      console.dir('Ошибка сервера!');
  }
  throw err;
}


export default {
  get: (url, params) => axios.get(url, { params }).catch(errorHandler),
  post: (url, data) => axios.post(url, data).catch(errorHandler),
  put: (url, data) => axios.put(url, data).catch(errorHandler),
  delete: (url, params) => axios.delete(url, { params }).catch(errorHandler),
};
