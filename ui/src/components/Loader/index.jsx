import React from 'react';
import PropTypes from 'prop-types';
import cn from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';


const styles = () => ({
  container: {
    width: '100%',
    height: '100%',
    display: 'flex',
    position: 'absolute',
    alignItems: 'center',
    justifyContent: 'center',
  },
});


function Loader({ classes, className, size, thickness }) {
  return (
    <div className={cn(classes.container, className)}>
      <CircularProgress size={size} thickness={thickness} />
    </div>
  );
}

Loader.defaultProps = {
  size: 30,
  thickness: 4,
};

Loader.propTypes = {
  className: PropTypes.object,
  size: PropTypes.number,
  thickness: PropTypes.number,
};

export default withStyles(styles)(Loader);
