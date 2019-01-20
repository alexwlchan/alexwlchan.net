Jekyll::Hooks.register :site, :post_read do |site|
  site.collections["microposts"]
    .docs
    .sort_by! { |micropost| micropost.date }
    .each
    .with_index(1) { |micropost, mp_number|
      micropost.data["is_micropost"] = true
      micropost.data["micropost_number"] = mp_number
    }
end
