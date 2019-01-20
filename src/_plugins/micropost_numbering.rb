Jekyll::Hooks.register :site, :post_read do |site|
  site.collections["microposts"]
    .docs
    .sort_by! { |micropost| micropost.date }
    .each
    .with_index(1) { |micropost, mp_number|

      # Was this micropost title created automatically?  If so, let's ditch
      # it -- we don't actually want it.
      if micropost.data["title"] == Jekyll::Utils.titleize_slug(micropost.data["slug"])
        micropost.data.delete("title")
      end

      micropost.data["is_micropost"] = true
      micropost.data["micropost_number"] = mp_number
    }
end
