# Temporary code editing and highlighting

Approved in chat: highlight all six languages and read-only notes pseudocode; make only starter templates editable. Keep each problem/language draft in the current DOM, preserve drafts across tab changes, restore templates on refresh, and provide copy/reset. No code execution, backend, CDN, or code persistence. The existing language preference remains persisted.

Approach: extend the existing app.js and style.css with a small lexical highlighter and a native textarea over a matching highlighted preview. Compared with a full editor library, this keeps the static site dependency-free; it provides indentation and normal textarea editing without IDE features. Reference answers and no-JS code remain readable. The generator remains the source of exercise markup.
