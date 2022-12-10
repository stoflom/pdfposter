;; Per-directory local variables for GNU Emacs 23 and later.

(
 (nil
  . ((fill-column . 78)
     (tab-width   .  4)
     (ispell-check-comments . exclusive)
     (ispell-local-dictionary . "en_US")
     (indent-tabs-mode . nil)
     (safe-local-variable-values
      '(sentence-end-double-space . t)
      (eval add-hook 'rst-mode-hook #'flyspell-mode)
      (eval add-hook 'text-mode-hook #'flyspell-mode)
      (eval add-hook 'c-mode-hook #'flyspell-prog-mode)
      (eval add-hook 'python-mode-hook #'flyspell-prog-mode)
      (flyspell-issue-message-flag . f) ; avoid messages for every word
      )))
 (makefile-mode . ((indent-tabs-mode . t)))
)
