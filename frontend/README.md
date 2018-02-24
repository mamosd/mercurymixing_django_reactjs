# Mercury Mixing Frontend

Scripts and styles for the Mercury Mixing website. The frontend is divided in
two main sections (corresponding to the generated bundles):

- `app/index.js`: The modern Preact (React) + Redux application that allows
  users to upload their files for mixing. Generates `mixing.js` and
  `mixing.css`.

- `classic/index.js`: The classic, site-wide scripts and styles for regular
  site pages. Generates `classic.js` and `classic.css`.

## Development Workflow

**0. Install all npm dependencies when running for the first time**:
`npm install`

**1. Start a live-reload development server:**

```sh
PORT=8080 npm run dev
```

> This is a full web server nicely suited to your project. Any time you make
> changes within the `app`, `styles`, and `classic` directories, it will
> rebuild and even refresh your browser.

In the Django template, you only need to include two `<script>` tags pointing
to `http://localhost:8080/classic.js` and `mixing.js`. Of course, this only
works for development, where the Webpack server is running. Visit the Django
server (usually running in port 8000) to develop the app.

Keep in mind that Webpack Dev Server will automatically insert styles when
you include the `<script>` tags, and hot code reloading will work for both
styles and scripts.

**2. Generate a production build in `/mixing/static/build`:**

```sh
npm run build
```

The resulting files are now in a path the Django's `collectstatic` can
understand. The file names will be the same as before. You'll need to update
the Django templates to fetch the scripts as any other static file, not from
`localhost:8080`. For example:

```django
<script src="{% static 'build/classic.js' %}"></script>
<script src="{% static 'build/mixing.js' %}"></script>
```

You'll also want to include the styles in the `<head>` of the document, which
will not be auto-inserted any more in production:

```django
<link rel="stylesheet" href="{% static 'build/classic.css' %}">
<link rel="stylesheet" href="{% static 'build/mixing.css' %}">
```
