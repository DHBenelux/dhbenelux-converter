function Image( element )
      prepend_path = ""
      image = pandoc.Image( element.caption, element.src, element.title )
      image.src = prepend_path .. element.src
      image.identifier = element.identifier
      return image
    end
    