import React from 'react';
import PropTypes from 'prop-types';


// TODO: make loader component
export default function Loader({ className }) {
  return <div className={className}>Loading...</div>;
}

Loader.propTypes = {
  className: PropTypes.object,
};
