import { useState } from 'react';
import { Modal } from '../../components/ui/modal';
import { Button } from '../../components/ui/button';
import { CodeEditor } from './CodeEditor';
import { useCodeGeneration } from './useCodeGeneration';

export const CodeGenerationModal = ({ analysisId }) => {
  const [open, setOpen] = useState(false);
  const { code, isGenerating, generateCode } = useCodeGeneration();

  return (
    <>
      <Button variant="secondary" onClick={() => setOpen(true)}>
        Generate fix
      </Button>
      <Modal
        isOpen={open}
        onClose={() => setOpen(false)}
        title="Code suggestions"
        description="AI-generated remediation tailored to your dataset."
        footer={
          <>
            <Button variant="secondary" onClick={() => setOpen(false)}>
              Close
            </Button>
            <Button onClick={() => generateCode(analysisId)} disabled={isGenerating}>
              {isGenerating ? 'Generating…' : 'Regenerate'}
            </Button>
          </>
        }
      >
        <CodeEditor value={code} />
      </Modal>
    </>
  );
};

