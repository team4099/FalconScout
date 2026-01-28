import React from 'react';
import { useTheme } from '../ThemeContext';
import { ComponentSetup } from '../interface';

function SubmitButton(props: ComponentSetup) {
  const { theme } = useTheme();

  const buttonStyle = {
    padding: '10px 20px',
    borderRadius: '0.5rem',
    border: '1px solid var(--input-border-color)',
    backgroundColor: 'var(--input-bg-color)',
    color: 'var(--input-text-color)',
    cursor: 'pointer',
    fontSize: '1rem',
    fontWeight: '600',
  };

  const handleClick = () => {
    // Set result to true to trigger the QR code modal
    props.getValue.result = true;
    props.setValue(props.getValue);
  };

  return (
    <div className="mx-3 my-3">
      <button style={buttonStyle} onClick={handleClick}>
        {props.text || 'Submit'}
      </button>
    </div>
  );
}

export default SubmitButton;
