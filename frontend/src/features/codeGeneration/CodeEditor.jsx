export const CodeEditor = ({ value = '' }) => (
  <pre className="max-h-96 overflow-auto rounded-xl bg-gray-900 p-4 text-xs text-green-200">
    {value || '// Press "Generate" to see AI suggestions'}
  </pre>
);

