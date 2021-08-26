import axios from 'axios';
import qs from 'qs';

const API_ENDPOINT = process.env.REACT_APP_API_ENDPOINT;

function getCookie(name) {
  const cookie = {};
  document.cookie.split(';').forEach((el) => {
    const [k, v] = el.split('=');
    cookie[k.trim()] = v;
  });
  return cookie[name];
}

const fetchClient = () => {
  const defaultOptions = {
    baseURL: API_ENDPOINT,
    headers: {
      'Content-Type': 'application/json',
    },
    paramsSerializer: params => {
      return qs.stringify(params)
    },
  };

  let instance = axios.create(defaultOptions);

  instance.interceptors.request.use(function (config) {
    const csrftoken = getCookie('csrftoken');
    if (csrftoken !== undefined) {
      config.headers['X-CSRFToken'] = csrftoken;
    }
    return config;
  });
  instance.interceptors.response.use((response) => {
    return response;
  }, (error) => {
    if (401 === error.response.status) {
      window.location = '/login';
      return Promise.reject(error);
    } else {
      return Promise.reject(error);
    }
  });

  return instance;
};

export default fetchClient();
