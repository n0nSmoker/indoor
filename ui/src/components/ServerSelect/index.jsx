import React from 'react';
import PropTypes from 'prop-types';
import cn from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import IconButton from '@material-ui/core/IconButton';
import Popper from '@material-ui/core/Popper';
import Paper from '@material-ui/core/Paper';
import CloseIcon from '@material-ui/icons/Close';
import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';

import requests from 'lib/requests';

import styles from './styles';


class ServerSelect extends React.Component {
  inputRef = React.createRef();
  optionsRef = React.createRef();

  constructor(props) {
    super(props);
    const { initialValue, valueKey, labelKey } = props;
    this.state = {
      showOptions: false,
      options: [],
      ...(
        initialValue
          ? {
            selectedOption: {
              value: initialValue[valueKey],
              label: initialValue[labelKey],
            },
            value: initialValue[labelKey],
          }
          : {
            selectedOption: null,
            value: '',
          }
      ),
    };
  }

  componentDidMount() {
    this.getOptions();
  }

  getOptions = query => {
    const { path, valueKey, labelKey, optionsLimit: limit } = this.props;
    requests.get(`/${path}/`, { query, limit }).then(({ data: { results } }) => {
      this.setState({
        options: results.map(item => ({
          value: item[valueKey],
          label: item[labelKey],
        }))
      });
    });
  };

  componentWillUnmount() {
    document.removeEventListener('click', this.handleOutsideClick, false);
  }

  clear = () => {
    this.setState({ value: '', selectedOption: null });
    this.getOptions();
  };

  handleOutsideClick = ({ target }) => {
    if (this.optionsRef.current.contains(target) || this.inputRef.current.contains(target)) return;
    this.toggleShowOptions();
  };

  toggleShowOptions = () => {
    const showOptions = !this.state.showOptions;
    this.setState({ showOptions });
    if (showOptions) {
      document.addEventListener('click', this.handleOutsideClick, false);
    } else {
      document.removeEventListener('click', this.handleOutsideClick, false);
    }
  };

  handleSelect = option => () => {
    const { onChange, name } = this.props;
    this.setState(() => ({
      value: option.label,
      selectedOption: option,
      showOptions: false,
    }));
    onChange({
      target: {
        name,
        value: option.value,
      },
    });
  };

  handleInputChange = ({ target: { value } }) => {
    this.setState(() => ({
      value,
      selectedOption: null,
    }));
    if (2 < value.length || !value) {
      this.getOptions(value);
    }
  };

  renderPopper = () => {
    const { options, selectedOption } = this.state;
    const { classes } = this.props;
    return (
      <Popper
        open
        anchorEl={this.inputRef.current}
        ref={this.optionsRef}
        className={classes.popper}
        style={{
          width: this.inputRef.current.clientWidth,
        }}
      >
        <Paper className={classes.paper}>
          {options.length
            ? (
              <ul className={classes.optionsList}>
                {options.map(item => {
                  const isSelected = selectedOption && selectedOption.value === item.value;
                  return (
                    <li
                      key={item.value}
                      className={cn(classes.option, isSelected ? 'selected' : null)}
                      onClick={this.handleSelect(item)}
                    >
                      {item.label}
                    </li>
                  );
                })}
              </ul>
            )
            : <div className={classes.noResults}>Нет результатов</div>
          }
        </Paper>
      </Popper>
    );
  };

  render() {
    const { showOptions, value } = this.state;
    const { classes, label, variant, margin } = this.props;
    return (
      <>
        <TextField
          fullWidth
          variant={variant}
          margin={margin}
          label={label}
          onChange={this.handleInputChange}
          value={value}
          onFocus={!showOptions ? this.toggleShowOptions : null}
          ref={this.inputRef}
          InputProps={{
            classes: {
              root: classes.root,
            },
            endAdornment: (
              <>
                {value &&
                  <IconButton
                    onClick={this.clear}
                    className={classes.adornment}
                  >
                    <CloseIcon />
                  </IconButton>}
                <IconButton
                  className={classes.adornment}
                  onClick={this.toggleShowOptions}
                >
                  <ArrowDropDownIcon />
                </IconButton>
              </>
            ),
          }}
        />
        {showOptions && this.renderPopper()}
      </>
    );
  }
}

ServerSelect.defaultProps = {
  variant: 'outlined',
  margin: 'dense',
  valueKey: 'id',
  labelKey: 'id',
  onChange: console.log,
  optionsLimit: 25,
};

ServerSelect.propTypes = {
  classes: PropTypes.object.isRequired,
  path: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  optionsLimit: PropTypes.number,
  onChange: PropTypes.func,
  label: PropTypes.string,
  variant: PropTypes.string,
  margin: PropTypes.string,
  valueKey: PropTypes.string,
  labelKey: PropTypes.string,
};

export default withStyles(styles)(ServerSelect);
