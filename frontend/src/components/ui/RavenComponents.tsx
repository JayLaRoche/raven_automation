import React, { ReactNode, ButtonHTMLAttributes, InputHTMLAttributes, HTMLAttributes } from 'react';

/**
 * Button Component - Raven Custom Glass Brand Styling
 * Supports multiple variants and sizes
 */
export function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  className = '',
  ...props
}: {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'tertiary' | 'danger' | 'success';
  size?: 'sm' | 'md' | 'lg' | 'xl';
  disabled?: boolean;
  className?: string;
} & ButtonHTMLAttributes<HTMLButtonElement>) {
  const baseStyles = `
    inline-flex items-center justify-center
    font-semibold rounded-base
    transition-all duration-150 ease-out
    cursor-pointer
    focus:outline-none focus:ring-2 focus:ring-raven-black focus:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed
  `;

  const variants = {
    primary: `
      bg-raven-black text-raven-white
      hover:bg-raven-800 active:bg-raven-900
      shadow-sm hover:shadow-md
    `,
    secondary: `
      bg-transparent border-2 border-raven-gray-200 text-raven-gray-900
      hover:bg-raven-gray-50 hover:border-raven-gray-300
      active:bg-raven-gray-100
    `,
    tertiary: `
      bg-transparent text-raven-black
      hover:text-raven-gray-700
      focus:text-raven-black
    `,
    danger: `
      bg-raven-error text-raven-white
      hover:bg-red-600 active:bg-red-700
      shadow-sm hover:shadow-md
    `,
    success: `
      bg-raven-success text-raven-white
      hover:bg-green-500 active:bg-green-700
      shadow-sm hover:shadow-md
    `,
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg',
    xl: 'px-10 py-5 text-xl',
  };

  const combinedClassName = `
    ${baseStyles}
    ${variants[variant] || variants.primary}
    ${sizes[size] || sizes.md}
    ${className}
  `;

  return (
    <button
      className={combinedClassName}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
}

/**
 * Input Component - Raven Custom Glass Brand Styling
 * Handles text, email, password, number inputs
 */
export function Input({
  type = 'text',
  placeholder = '',
  disabled = false,
  error = '',
  label = '',
  className = '',
  ...props
}: {
  type?: string;
  placeholder?: string;
  disabled?: boolean;
  error?: string;
  label?: string;
  className?: string;
} & InputHTMLAttributes<HTMLInputElement>) {
  const baseStyles = `
    w-full px-3.5 py-2.5
    text-base text-raven-gray-900
    placeholder:text-raven-gray-400
    border-2 border-raven-gray-300 rounded-base
    bg-raven-white
    transition-all duration-150 ease-out
    focus:outline-none focus:border-raven-black focus:ring-2 focus:ring-raven-black focus:ring-offset-2
    disabled:bg-raven-gray-100 disabled:text-raven-gray-400 disabled:cursor-not-allowed
  `;

  const errorStyles = error
    ? 'border-raven-error focus:border-raven-error focus:ring-raven-error'
    : '';

  const combinedClassName = `
    ${baseStyles}
    ${errorStyles}
    ${className}
  `;

  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-raven-gray-900 mb-2">
          {label}
        </label>
      )}
      <input
        type={type}
        placeholder={placeholder}
        disabled={disabled}
        className={combinedClassName}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-raven-error">{error}</p>
      )}
    </div>
  );
}

/**
 * Card Component - Raven Custom Glass Brand Styling
 * Container for grouped content
 */
export function Card({
  children,
  className = '',
  elevated = false,
  ...props
}: {
  children: ReactNode;
  className?: string;
  elevated?: boolean;
} & HTMLAttributes<HTMLDivElement>) {
  const baseStyles = `
    bg-raven-white
    border-2 border-raven-gray-200 rounded-lg
    p-6
    transition-all duration-200 ease-out
  `;

  const elevatedStyles = elevated
    ? 'hover:shadow-lg hover:border-raven-gray-300'
    : '';

  return (
    <div
      className={`${baseStyles} ${elevatedStyles} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

/**
 * Header Component - Raven Custom Glass Brand Header
 * Navigation bar with logo and CTA
 */
export function Header({
  logoText = "Raven's Design Sandbox",
  navLinks = [],
  ctaButton = null,
}: Readonly<{
  logoText?: string;
  navLinks?: { id: string | number; href: string; label: string }[];
  ctaButton?: string | null;
}>) {
  return (
    <header className="w-full bg-raven-white border-b border-raven-gray-200 sticky top-0 z-50 shadow-sm">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center">
          <h1 className="text-2xl font-bold text-raven-black">
            {logoText}
          </h1>
        </div>

        {/* Navigation */}
        <nav className="hidden md:flex gap-8">
          {navLinks.map((link) => (
            <a
              key={link.id}
              href={link.href}
              className="
                text-raven-gray-900 font-medium
                hover:text-raven-black
                transition-colors duration-150
                relative
                after:absolute after:bottom-0 after:left-0 after:h-0.5
                after:bg-raven-black after:w-0
                after:transition-all after:duration-150
                hover:after:w-full
              "
            >
              {link.label}
            </a>
          ))}
        </nav>

        {/* CTA Button */}
        {ctaButton && (
          <div className="ml-auto">
            <Button variant="primary" size="md">
              {ctaButton}
            </Button>
          </div>
        )}
      </div>
    </header>
  );
}

/**
 * Footer Component - Raven Custom Glass Brand Footer
 */
export function Footer({
  companyName = 'Raven Custom Glass',
  address = '9960 W Cheyenne Ave, Suite 140, Las Vegas NV 89129',
  phone = '(702) 577-1003',
  ctaButton = null,
  links = [],
}: Readonly<{
  companyName?: string;
  address?: string;
  phone?: string;
  ctaButton?: string | null;
  links?: Array<{ title: string; items: { id: string | number; href: string; label: string }[] }>;
}>) {
  return (
    <footer className="w-full bg-raven-gray-900 text-raven-gray-100 border-t border-raven-gray-700">
      <div className="container mx-auto px-4 py-12">
        {/* Content Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Company Info */}
          <div>
            <h3 className="text-lg font-bold text-raven-white mb-4">
              {companyName}
            </h3>
            <p className="text-sm text-raven-gray-300 mb-3">{address}</p>
            <p className="text-sm text-raven-gray-300">
              <a
                href={`tel:${phone}`}
                className="hover:text-raven-white transition-colors"
              >
                {phone}
              </a>
            </p>
          </div>

          {/* Links Columns */}
          {links.map((column, idx) => (
            <div key={idx}>
              <h4 className="text-sm font-semibold text-raven-white mb-3">
                {column.title}
              </h4>
              <ul className="space-y-2">
                {column.items.map((item) => (
                  <li key={item.id}>
                    <a
                      href={item.href}
                      className="text-sm text-raven-gray-300 hover:text-raven-white transition-colors"
                    >
                      {item.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Divider */}
        <div className="border-t border-raven-gray-700 pt-8 mt-8">
          {/* Bottom Footer */}
          <div className="flex flex-col md:flex-row items-center justify-between">
            <p className="text-sm text-raven-gray-400">
              &copy; 2025 {companyName}. All rights reserved.
            </p>

            {/* Social Links */}
            <div className="flex gap-4 mt-4 md:mt-0">
              {['Facebook', 'Instagram', 'LinkedIn'].map((social) => (
                  <button
                    key={social}
                    className="text-raven-gray-400 hover:text-raven-white transition-colors bg-none border-none cursor-pointer p-0"
                  >
                    {social}
                  </button>
                ))}
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

/**
 * Section Component - Raven Custom Glass Section Container
 * Used for main content sections
 */
export function Section({
  children,
  title = '',
  subtitle = '',
  className = '',
  background = 'white',
  ...props
}: {
  children: ReactNode;
  title?: string;
  subtitle?: string;
  className?: string;
  background?: 'white' | 'gray';
} & HTMLAttributes<HTMLElement>) {
  const bgColor = background === 'gray'
    ? 'bg-raven-gray-50'
    : 'bg-raven-white';

  return (
    <section className={`w-full py-12 md:py-16 lg:py-20 ${bgColor}`}>
      <div className={`container mx-auto px-4 ${className}`}>
        {title && (
          <div className="mb-8 md:mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-raven-black mb-2">
              {title}
            </h2>
            {subtitle && (
              <p className="text-lg text-raven-gray-600">
                {subtitle}
              </p>
            )}
          </div>
        )}
        {children}
      </div>
    </section>
  );
}

/**
 * Badge Component - For labels and status indicators
 */
export function Badge({
  children,
  variant = 'default',
  size = 'md',
  className = '',
}: Readonly<{
  children: ReactNode;
  variant?: 'default' | 'primary' | 'success' | 'error' | 'warning' | 'info';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}>) {
  const variants = {
    default: 'bg-raven-gray-200 text-raven-gray-900',
    primary: 'bg-raven-black text-raven-white',
    success: 'bg-raven-success text-raven-white',
    error: 'bg-raven-error text-raven-white',
    warning: 'bg-raven-warning text-raven-white',
    info: 'bg-raven-info text-raven-white',
  };

  const sizes = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1.5 text-sm',
    lg: 'px-4 py-2 text-base',
  };

  return (
    <span
      className={`
        inline-flex items-center
        rounded-full font-semibold
        ${variants[variant]}
        ${sizes[size]}
        ${className}
      `}
    >
      {children}
    </span>
  );
}

/**
 * Divider Component
 */
export function Divider({ className = '' }: { className?: string }) {
  return (
    <div className={`w-full h-px bg-raven-gray-200 ${className}`} />
  );
}

/**
 * Skeleton/Loading Component
 */
export function Skeleton({
  width = 'w-full',
  height = 'h-4',
  rounded = 'rounded-base',
  className = '',
}: {
  width?: string;
  height?: string;
  rounded?: string;
  className?: string;
}) {
  return (
    <div
      className={`
        ${width} ${height} ${rounded}
        bg-gradient-to-r from-raven-gray-200 via-raven-gray-100 to-raven-gray-200
        animate-pulse
        ${className}
      `}
    />
  );
}
