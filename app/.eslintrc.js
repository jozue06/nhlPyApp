module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
    jest: true,
  },
  extends: ['react-app', 'react-app/jest', 'prettier'],
  plugins: ['prettier'],
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: 'module',
  },
  rules: {
    // Prettier integration
    'prettier/prettier': 'error',

    // Quote style (enforce double quotes to match Prettier)
    quotes: [
      'error',
      'double',
      { avoidEscape: true, allowTemplateLiterals: true },
    ],

    // Indentation rules (enforce 2 spaces)
    indent: [
      'error',
      2,
      {
        SwitchCase: 1,
        VariableDeclarator: 1,
        outerIIFEBody: 1,
        MemberExpression: 1,
        FunctionDeclaration: { parameters: 1, body: 1 },
        FunctionExpression: { parameters: 1, body: 1 },
        CallExpression: { arguments: 1 },
        ArrayExpression: 1,
        ObjectExpression: 1,
        ImportDeclaration: 1,
        flatTernaryExpressions: false,
        ignoreComments: false,
      },
    ],

    // React specific rules
    'react/jsx-uses-react': 'error',
    'react/jsx-uses-vars': 'error',
    'react/prop-types': 'off', // Turn off if not using PropTypes
    'react/jsx-indent': ['error', 2],
    'react/jsx-indent-props': ['error', 2],

    // JavaScript best practices
    'no-unused-vars': 'warn',
    'no-console': 'warn',
    'no-debugger': 'error',

    // Code style
    'prefer-const': 'error',
    'no-var': 'error',
    'object-shorthand': 'error',
    'prefer-template': 'error',

    // React Hooks
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',

    // Consistent bracing (enforce our recent changes)
    curly: ['error', 'all'],
    'brace-style': ['error', '1tbs', { allowSingleLine: false }],

    // Spacing and formatting
    'no-multiple-empty-lines': ['error', { max: 1, maxEOF: 0 }],
    'space-before-blocks': 'error',
    'keyword-spacing': 'error',
    'space-infix-ops': 'error',
    'comma-spacing': 'error',
    'object-curly-spacing': ['error', 'always'],
    'array-bracket-spacing': ['error', 'never'],
    'computed-property-spacing': ['error', 'never'],
    'space-in-parens': ['error', 'never'],
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
