class Astra < Formula
  desc "Astra: A Powerful Network Scanner"
  homepage "https://github.com/bhaweshchaudhary/astra"
  url "https://github.com/bhaweshchaudhary/astra/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "replace_with_actual_sha256"
  license "MIT"

  depends_on "python@3.9"

  def install
    system "python3", "setup.py", "install", "--prefix=#{prefix}"
  end

  test do
    system "#{bin}/astra", "--help"
  end
end