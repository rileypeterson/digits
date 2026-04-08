# Digits

Numbers game based on NYT digits which was discontinued.

<img width="1341" height="728" alt="image" src="https://github.com/user-attachments/assets/d4991d00-e2f6-4f69-8777-3c59f5a17066" />

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

### Push to gh-pages branch
```
npm run build
# Comment out dist in gitignore
git add dist && git commit -m 'adding dist subtree'
git push origin `git subtree split --prefix dist main`:gh-pages --force
git reset --hard origin/main
```
