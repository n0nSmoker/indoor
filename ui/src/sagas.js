import usersSagas from './pages/Users/sagas';


export default function runSagas(sagaMiddleware) {
  sagaMiddleware.run(usersSagas);
}
