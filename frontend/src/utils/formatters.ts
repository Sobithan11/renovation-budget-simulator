export function formatCurrency(value: number) {
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP',
    maximumFractionDigits: 0,
  }).format(value)
}

export function formatPercentage(value: number) {
  return `${(value * 100).toFixed(1)}%`
}