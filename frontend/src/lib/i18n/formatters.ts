import { Language, DisplayCurrency } from './translations';
import { REGULATORY_CONFIG } from '../config/regulatory';

const BENGALI_DIGITS: Record<string, string> = {
  '0': '০',
  '1': '১',
  '2': '২',
  '3': '৩',
  '4': '৪',
  '5': '৫',
  '6': '৬',
  '7': '৭',
  '8': '৮',
  '9': '৯',
};

/**
 * Converts Western digits 0-9 to Eastern Bengali digits ০-৯
 */
export function toBengaliDigits(input: string | number): string {
  const str = input.toString();
  return str.replace(/[0-9]/g, (match) => BENGALI_DIGITS[match] || match);
}

/**
 * Formats a currency amount given in BDT base into either BDT or USD,
 * respecting the active language and official Bangladesh Bank interbank exchange rate.
 */
export function formatCurrencyAmount(
  amountBdt: number,
  currency: DisplayCurrency = 'BDT',
  language: Language = 'en'
): string {
  const rate = REGULATORY_CONFIG?.fxRatePolicy?.usdToBdt || 120.00; // 120.00 BDT/USD

  if (currency === 'BDT') {
    const formattedNum = Math.round(amountBdt).toLocaleString('en-IN');
    if (language === 'bn') {
      return `৳${toBengaliDigits(formattedNum)}`;
    }
    return `৳${formattedNum}`;
  }

  // Convert to USD
  const amountUsd = amountBdt / rate;
  const formattedUsd = amountUsd.toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

  if (language === 'bn') {
    return `$${toBengaliDigits(formattedUsd)}`;
  }
  return `$${formattedUsd}`;
}

/**
 * Returns dual-currency breakdown (Primary BDT and Secondary USD)
 */
export function formatDualCurrency(
  amountBdt: number,
  language: Language = 'en'
): { primary: string; secondary: string } {
  return {
    primary: formatCurrencyAmount(amountBdt, 'BDT', language),
    secondary: formatCurrencyAmount(amountBdt, 'USD', language),
  };
}
