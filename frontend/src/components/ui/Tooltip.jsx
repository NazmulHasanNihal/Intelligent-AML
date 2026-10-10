import React, { useState } from 'react';

export const Tooltip = ({
  content,
  children,
  side = 'top', // 'top' | 'bottom' | 'left' | 'right'
  delay = 200,
  className = ''
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const [timeoutId, setTimeoutId] = useState(null);

  if (!content) return <>{children}</>;

  const handleMouseEnter = () => {
    const id = setTimeout(() => setIsVisible(true), delay);
    setTimeoutId(id);
  };

  const handleMouseLeave = () => {
    if (timeoutId) clearTimeout(timeoutId);
    setIsVisible(false);
  };

  const sidePositions = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-1.5',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-1.5',
    left: 'right-full top-1/2 -translate-y-1/2 mr-1.5',
    right: 'left-full top-1/2 -translate-y-1/2 ml-1.5'
  };

  return (
    <div
      className={`relative inline-flex items-center ${className}`}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onFocus={handleMouseEnter}
      onBlur={handleMouseLeave}
    >
      {children}
      {isVisible && (
        <div
          role="tooltip"
          className={`absolute ${sidePositions[side]} z-50 px-2 py-1 text-[10px] font-medium text-white bg-neutral-900 dark:bg-neutral-800 rounded shadow-md pointer-events-none whitespace-nowrap border border-white/10 animate-in fade-in zoom-in-95 duration-100`}
        >
          {content}
        </div>
      )}
    </div>
  );
};
