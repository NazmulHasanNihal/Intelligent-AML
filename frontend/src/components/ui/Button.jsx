import React from 'react';

export const Button = React.forwardRef(({
  children,
  variant = 'secondary', // 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'subtle'
  size = 'md', // 'sm' | 'md' | 'lg' | 'icon'
  className = '',
  disabled = false,
  onClick,
  type = 'button',
  icon: Icon,
  ...props
}, ref) => {
  const baseStyles = "inline-flex items-center justify-center font-medium transition-colors select-none rounded focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-50 disabled:pointer-events-none active:translate-y-px";

  const sizeStyles = {
    sm: "text-xs px-2.5 py-1 gap-1.5 h-7",
    md: "text-xs px-3 py-1.5 gap-2 h-8",
    lg: "text-sm px-4 py-2 gap-2 h-9",
    icon: "h-8 w-8 p-0"
  };

  const variantStyles = {
    primary: "bg-accent hover:bg-accent-hover text-white shadow-sm border border-transparent font-semibold",
    secondary: "bg-surface hover:bg-surfaceHover text-text border border-border shadow-sm",
    outline: "bg-transparent hover:bg-surfaceHover text-text border border-border",
    ghost: "bg-transparent hover:bg-surfaceHover text-text-2 hover:text-text",
    danger: "bg-critical hover:bg-critical-text text-white shadow-sm border border-transparent font-semibold",
    subtle: "bg-accent-subtle text-accent-text hover:bg-accent/20 border border-transparent font-semibold"
  };

  return (
    <button
      ref={ref}
      type={type}
      disabled={disabled}
      onClick={onClick}
      className={`${baseStyles} ${sizeStyles[size]} ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {Icon && <Icon className="w-3.5 h-3.5 shrink-0" />}
      {children}
    </button>
  );
});

Button.displayName = 'Button';
