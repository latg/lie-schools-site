# Сайт школ-конференций "Алгебры Ли, алгебраические группы и теория инвариантов"

## Build

Use Hugo **0.59.1** and `rsync`. Run commands from the repository root.

```sh
sh build.sh
```

This builds `public/` with the existing local photo links and photo files.
Plain `hugo` also keeps the existing behavior used by the VPS workflow.

To serve photos from an external bucket:

```sh
HUGO_PARAMS_PHOTOBASEURL=https://your-bucket.s3.cloud.ru sh build.sh
```

The URL selects the external mode. Pages marked `photo = true` use it for
photos, thumbnails, and group photographs. The bucket must mirror the paths
under `static/`, including years, letter case, spaces, and filenames. For
example, `static/2009/Photos/1.jpg` must be available at
`https://your-bucket.s3.cloud.ru/2009/Photos/1.jpg`. A trailing slash on the
base URL is optional. Existing links to external albums stay unchanged.

The wrapper stages static files without gallery photos in external mode, so
Hugo does not copy the large originals into `public/`. Gallery
HTML, logos, posters, styles, and other site files remain. Source photos stay
in the repository. Switching back to the default build restores the local
images, including when reusing the same output directory.

Use the environment variable above to select external mode for `build.sh`;
the empty `params.photoBaseURL` in `config.toml` is the default.

## GitHub Pages

Before deploying, upload the photo files to the public bucket and set the
repository Actions variable **`PHOTO_BASE_URL`** to its public HTTPS URL.
Choose **Settings → Pages → Source → GitHub Actions**. If using
`lie-school.ru`, configure that custom domain and its DNS in Pages settings.

The separate `Publish to GitHub Pages` workflow runs on pushes to `main` or
manually. It builds without the photo files and publishes `public/`. It uses
the URL from Pages settings and adjusts root-relative site links during
the build. It stops with an error if `PHOTO_BASE_URL` is missing. The workflow
does not upload photos to Cloud.ru.

The VPS workflow also runs only on `main`; pushing a development branch does
not deploy it.

## Check

With Hugo 0.59.1 on `PATH`:

```sh
python3 -m unittest discover -s tests
```

The checks build temporary copies using the real content and asset paths,
with tiny placeholder assets. They verify local and external links, gallery
pages, photo exclusion, and switching back to a local build.


