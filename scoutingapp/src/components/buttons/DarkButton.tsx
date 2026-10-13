import React from 'react';
import { useTheme } from '../ThemeContext';

function DarkButton() {
  const { theme, toggleTheme } = useTheme();

  const buttonStyle = {
    padding: '8px 16px',
    borderRadius: '0.5rem',
    border: '1px solid var(--input-border-color)',
    backgroundColor: 'var(--input-bg-color)',
    color: 'var(--input-text-color)',
    cursor: 'pointer',
    fontSize: '0.875rem',
  };

  return (
    <button style={buttonStyle} onClick={toggleTheme}>
      {theme === 'light' ? '🌙' : '☀️'}
    </button>
  );
}

export default DarkButton;
