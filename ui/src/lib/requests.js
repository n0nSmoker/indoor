import axios from 'axios';


function errorHandler(err) {
  const { response } = err;
  if (response.status === 403) {
      window.location = '/';
  }
  throw err;
}


export default {
  get: (url, params) => axios.get(url, { params }).catch(errorHandler),
  post: (url, data, headers) => axios.post(url, data, { headers: headers }).catch(errorHandler),
  put: (url, data, headers) => axios.put(url, data, { headers: headers }).catch(errorHandler),
  delete: (url, params) => axios.delete(url, { params }).catch(errorHandler),
};
