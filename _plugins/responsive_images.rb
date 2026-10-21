# frozen_string_literal: true

# Responsive images for DScape.
#
# tools/make_variants.py writes smaller copies of each image into _variants/ and their sizes
# into _data/image_variants.json. This plugin
#   1. copies _variants/ into the site as /assets/img-v/, and
#   2. adds srcset, sizes, width and height to every <img> whose src has variants.
# Images without variants are left exactly as they are, so a missing variant never breaks a page.

module DScape
  IMG_TAG = /<img\b[^>]*>/i.freeze
  DEFAULT_SIZES = "(max-width: 800px) 100vw, 760px"

  # A static file read from _variants/ but written to /assets/img-v/.
  class VariantFile < Jekyll::StaticFile
    def initialize(site, base, dir, name, dest_dir)
      super(site, base, dir, name)
      @dest_dir = dest_dir
    end

    def destination(dest)
      File.join(dest, @dest_dir, @name)
    end

    def url
      File.join(@dest_dir, @name)
    end
  end

  class VariantGenerator < Jekyll::Generator
    safe true
    priority :low

    def generate(site)
      base = File.join(site.source, "_variants")
      return unless Dir.exist?(base)

      Dir.glob(File.join(base, "**", "*.webp")).each do |path|
        rel_dir = File.dirname(path).sub(base, "")
        site.static_files << VariantFile.new(site, site.source, File.join("_variants", rel_dir),
                                             File.basename(path), File.join("/assets/img-v", rel_dir))
      end
    end
  end

  def self.variant_url(src, width)
    src.sub(%r{\A/assets/img/}, "/assets/img-v/").sub(/\.[a-z]+\z/i, "-#{width}.webp")
  end

  def self.rewrite(html, manifest, baseurl)
    html.gsub(IMG_TAG) do |tag|
      src = tag[/\ssrc="([^"]+)"/, 1]
      next tag unless src

      key = src.sub(/\A#{Regexp.escape(baseurl)}/, "")
      info = manifest[key]
      next tag unless info

      out = tag.dup
      unless out.include?(" width=") || out.include?(" height=")
        out = out.sub(/<img\b/i, %(<img width="#{info['w']}" height="#{info['h']}"))
      end
      variants = Array(info["v"])
      unless variants.empty? || out.include?(" srcset=")
        set = variants.map { |w| "#{baseurl}#{variant_url(key, w)} #{w}w" }
        set << "#{src} #{info['w']}w"
        out = out.sub(/<img\b/i, %(<img srcset="#{set.join(', ')}"))
        out = out.sub(/<img\b/i, %(<img sizes="#{DEFAULT_SIZES}")) unless out.include?(" sizes=")
      end
      out
    end
  end
end

Jekyll::Hooks.register [:pages, :documents], :post_render do |doc|
  next unless doc.output_ext == ".html"

  manifest = doc.site.data["image_variants"]
  next unless manifest.is_a?(Hash) && !manifest.empty?

  doc.output = DScape.rewrite(doc.output, manifest, doc.site.baseurl.to_s)
end
