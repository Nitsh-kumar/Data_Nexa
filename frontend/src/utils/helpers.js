import clsx from 'clsx';

export const cn = (...inputs) => clsx(inputs);

export const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

