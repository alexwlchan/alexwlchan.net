from pathlib import Path

from jinja2 import Environment

from mosaic.models import CardConfig
from mosaic.pictures import create_image_derivatives


def article_card_image(env: Environment, src_dir: Path, out_dir: Path, card: CardConfig) -> str:
    derivatives, default_image = create_image_derivatives(
        src_path=src_dir / card.path,
        src_dir=src_dir,
        out_dir=out_dir,
        desired_widths=[
          365, 365 * 2,  # 2-up column => ~365px wide
          302, 302 * 2,  # 3-up column => ~302px wide
          405, 405 * 2 # 1-up column => ~405px wide
        ],
        out_path=Path("c") / (card.out_prefix + card.path.suffix)
    )

    template = env.get_template("partials/picture.html")
    return template.render(
        lt_derivatives=derivatives,
        default_image=default_image,
        #
        # There are two breakpoints for cards:
        #
        # * If the screen is 450px or narrower, there's only a single column
        #   of cards -- which take up almost all the screen width.
        # * If the screen is 1000px or narrower, there are two columns of
        #   cards, each of which takes up about half the screen
        # * If the screen is wider, there are three columns of cards,
        #   which all have a fixed width of ~300px
        #
        # However, we expand the default width to 370px to handle tag pages
        # which only have a small number of cards.
        sizes_attribute="(max-width:450px)100vw,(max-width:1000px)50vw,370px"
    )
