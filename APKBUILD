pkgname=jaraco-starter
pkgver=0.1.0
pkgrel=10
pkgdesc="Config-driven launcher for postmarketOS"
url="https://example.invalid/jaraco-starter"
arch="noarch"
license="MIT"
depends="python3 py3-gobject3 gtk4.0 libadwaita polkit"
makedepends="py3-setuptools"
options="!check"
source="$pkgname-$pkgver.tar.gz"

builddir="$srcdir/$pkgname-$pkgver"

prepare() {
    local _expected="$srcdir/$pkgname-$pkgver"
    if [ ! -d "$_expected" ]; then
        mkdir -p "$_expected"
        for _p in "$srcdir"/*; do
            [ -e "$_p" ] || continue
            [ "$_p" = "$_expected" ] && continue
            mv "$_p" "$_expected/"
        done
    fi
}

build() {
    return 0
}

package() {
    cd "$builddir"

    python3 setup.py install --root="$pkgdir" --prefix=/usr

    install -Dm755 src/jaraco_starter/runner.py "$pkgdir/usr/lib/jaraco-starter/runner"
    install -Dm644 data/io.jaraco.Starter.desktop "$pkgdir/usr/share/applications/io.jaraco.Starter.desktop"
    install -Dm644 data/io.jaraco.Starter.metainfo.xml "$pkgdir/usr/share/metainfo/io.jaraco.Starter.metainfo.xml"
    install -Dm644 data/io.jaraco.Starter.svg "$pkgdir/usr/share/icons/hicolor/scalable/apps/io.jaraco.Starter.svg"
    install -Dm644 data/io.jaraco.Starter.policy "$pkgdir/usr/share/polkit-1/actions/io.jaraco.Starter.policy"
    install -Dm644 starter.sample.json "$pkgdir/usr/share/jaraco-starter/starter.sample.json"
}
sha512sums="
48475be784195047e1f759f8d38b47eba6731ff1b088c3ad43ebb0c44f8d658fa082d567e5d2674969d8f043c57d58b4074eb4db7c969d41e06b30be71a79007  jaraco-starter-0.1.0.tar.gz
"
